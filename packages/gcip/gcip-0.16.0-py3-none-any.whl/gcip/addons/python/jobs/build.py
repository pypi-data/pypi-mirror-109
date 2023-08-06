from gcip.core.job import Job
from gcip.addons.python.scripts import (
    pip_install_requirements,
)


class BdistWheel(Job):
    def __init__(
        self,
        job_name: str = "bdist_wheel",
        job_stage: str = "build",
    ) -> None:
        """
        Runs `python3 setup.py bdist_wheel` and installs project requirements
        before (`scripts.pip_install_requirements()`)

        * Requires a `requirements.txt` in your project folder containing at least `setuptools`
        * Creates artifacts under the path `dist/`
        """
        super().__init__(
            name=job_name,
            stage=job_stage,
            script=[
                pip_install_requirements(),
                "python3 setup.py bdist_wheel",
            ],
        )
        self.artifacts.add_paths("dist/")
