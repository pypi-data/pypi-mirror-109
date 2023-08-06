# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean CLI v1.0. Copyright 2021 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import platform
import re
from pathlib import Path
from typing import Optional

import click

from lean.click import LeanCommand, PathParameter
from lean.container import container
from lean.models.docker import DockerImage

CUSTOM_FOUNDATION_IMAGE = DockerImage(name="lean-cli/foundation", tag="latest")
CUSTOM_ENGINE_IMAGE = DockerImage(name="lean-cli/engine", tag="latest")
CUSTOM_RESEARCH_IMAGE = DockerImage(name="lean-cli/research", tag="latest")


def _compile_csharp(root: Path, csharp_dir: Path) -> None:
    """Compiles C# code.

    :param csharp_dir: the directory containing the C# code
    """
    logger = container.logger()
    logger.info(f"Compiling the C# code in '{csharp_dir}'")

    build_path = Path("/LeanCLI") / csharp_dir.relative_to(root)

    docker_manager = container.docker_manager()
    docker_manager.create_volume("lean_cli_nuget")
    success = docker_manager.run_image(CUSTOM_FOUNDATION_IMAGE,
                                       entrypoint=["dotnet", "build", str(build_path)],
                                       environment={"DOTNET_CLI_TELEMETRY_OPTOUT": "true",
                                                    "DOTNET_NOLOGO": "true"},
                                       volumes={
                                           str(root): {
                                               "bind": "/LeanCLI",
                                               "mode": "rw"
                                           },
                                           "lean_cli_nuget": {
                                               "bind": "/root/.nuget/packages",
                                               "mode": "rw"
                                           }
                                       })

    if not success:
        raise RuntimeError("Something went wrong while running dotnet build, see the logs above for more information")


def _build_image(root: Path, dockerfile: Path, base_image: Optional[DockerImage], target_image: DockerImage) -> None:
    """Builds a Docker image.

    :param root: the path to build from
    :param dockerfile: the path to the Dockerfile to build
    :param base_image: the base image to use, or None if the default should be used
    :param target_image: the name of the new image
    """
    logger = container.logger()
    if base_image is not None:
        logger.info(f"Building '{target_image}' from '{dockerfile}' using '{base_image}' as base image")
    else:
        logger.info(f"Building '{target_image}' from '{dockerfile}'")

    if not dockerfile.is_file():
        raise RuntimeError(f"'{dockerfile}' does not exist")

    current_content = dockerfile.read_text(encoding="utf-8")

    if base_image is not None:
        new_content = re.sub(r"^FROM.*$", f"FROM {base_image}", current_content, flags=re.MULTILINE)
        dockerfile.write_text(new_content, encoding="utf-8")

    try:
        docker_manager = container.docker_manager()
        docker_manager.build_image(root, dockerfile, target_image)
    finally:
        if base_image is not None:
            dockerfile.write_text(current_content, encoding="utf-8")


@click.command(cls=LeanCommand, requires_docker=True)
@click.argument("root", type=PathParameter(exists=True, file_okay=False, dir_okay=True))
def build(root: Path) -> None:
    """Build Docker images of your own version of LEAN and the Alpha Streams SDK.

    \b
    ROOT must point to a directory containing the LEAN repository and the Alpha Streams SDK repository:
    https://github.com/QuantConnect/Lean & https://github.com/QuantConnect/AlphaStreams

    \b
    This command performs the following actions:
    1. The lean-cli/foundation:latest image is built from Lean/DockerfileLeanFoundation(ARM).
    2. LEAN is compiled in a Docker container using the lean-cli/foundation:latest image.
    3. The Alpha Streams SDK is compiled in a Docker container using the lean-cli/foundation:latest image.
    4. The lean-cli/engine:latest image is built from Lean/Dockerfile using lean-cli/foundation:latest as base image.
    5. The lean-cli/research:latest image is built from Lean/DockerfileJupyter using lean-cli/engine:latest as base image.
    6. The default engine image is set to lean-cli/engine:latest.
    7. The default research image is set to lean-cli/research:latest.
    """
    lean_dir = root / "Lean"
    if not lean_dir.is_dir():
        raise RuntimeError(f"Please clone https://github.com/QuantConnect/Lean to '{lean_dir}'")

    alpha_streams_dir = root / "AlphaStreams"
    if not lean_dir.is_dir():
        raise RuntimeError(f"Please clone https://github.com/QuantConnect/AlphaStreams to '{alpha_streams_dir}'")

    (root / "DataLibraries").mkdir(exist_ok=True)

    if platform.machine() in ["arm64", "aarch64"]:
        foundation_dockerfile = lean_dir / "DockerfileLeanFoundationARM"
    else:
        foundation_dockerfile = lean_dir / "DockerfileLeanFoundation"

    _build_image(root, foundation_dockerfile, None, CUSTOM_FOUNDATION_IMAGE)
    _compile_csharp(root, lean_dir)
    _compile_csharp(root, alpha_streams_dir)
    _build_image(root, lean_dir / "Dockerfile", CUSTOM_FOUNDATION_IMAGE, CUSTOM_ENGINE_IMAGE)
    _build_image(root, lean_dir / "DockerfileJupyter", CUSTOM_ENGINE_IMAGE, CUSTOM_RESEARCH_IMAGE)

    logger = container.logger()
    cli_config_manager = container.cli_config_manager()

    logger.info(f"Setting default engine image to '{CUSTOM_ENGINE_IMAGE}'")
    cli_config_manager.engine_image.set_value(str(CUSTOM_ENGINE_IMAGE))

    logger.info(f"Setting default research image to '{CUSTOM_RESEARCH_IMAGE}'")
    cli_config_manager.research_image.set_value(str(CUSTOM_RESEARCH_IMAGE))
