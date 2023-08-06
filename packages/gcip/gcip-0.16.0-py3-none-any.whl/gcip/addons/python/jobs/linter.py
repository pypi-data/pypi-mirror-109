from typing import Optional

from gcip.core.job import Job


class Flake8(Job):
    def __init__(
        self,
        job_name: str = "flake8",
        job_stage: str = "lint",
    ) -> None:
        """
        Runs:

        ```
        pip3 install --upgrade flake8
        flake8
        ```
        """
        super().__init__(
            name=job_name,
            stage=job_stage,
            script=[
                "pip3 install --upgrade flake8",
                "flake8",
            ],
        )


class Mypy(Job):
    def __init__(
        self,
        package_dir: str,
        mypy_version: str = "0.812",
        mypy_options: Optional[str] = None,
        job_name: str = "mypy",
        job_stage: str = "lint",
    ) -> None:
        """
        Install mypy if not already installed.
        Execute mypy for `package_dir`.

        Args:
            package_dir (str): Package directory to type check.
            mypy_version (str, optional): If `mypy` is not already installed this version will be installed. Defaults to "0.812".
            mypy_options (Optional[str], optional): Adds arguments to mypy execution. Defaults to None.
            job_name (str): The jobs name used in pipeline. Defaults to "mypy".
            job_stage (str): The jobs stage used in pipeline. Defaults to "lint".
        Returns:
            Job: gcip.Job
        """
        script = [f'pip3 freeze | grep -q "^mypy==" || pip3 install mypy=={mypy_version}']

        if mypy_options:
            script.append(f"mypy {mypy_options} {package_dir}")
        else:
            script.append(f"mypy {package_dir}")

        super().__init__(
            name=job_name,
            stage=job_stage,
            script=script,
        )


class Isort(Job):
    def __init__(
        self,
        job_name: str = "isort",
        job_stage: str = "lint",
    ) -> None:
        """
        Runs:

        ```
        pip3 install --upgrade isort
        isort --check .
        ```
        """
        super().__init__(
            name=job_name,
            stage=job_stage,
            script=[
                "pip3 install --upgrade isort",
                "isort --check .",
            ],
        )
