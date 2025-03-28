.. _contributing:

Contributing
=========================

We welcome contributions from the community! Whether you're fixing a bug, adding a feature, or improving documentation, your help is appreciated. Below are the steps to get started.

Setting Up the Development Environment
--------------------------------------

1. **Fork the Repository**: Start by forking the `inferplot` repository on GitHub.

2. **Clone Your Fork**: Clone your forked repository to your local machine.

   .. code-block:: bash

      git clone https://github.com/YOUR_USERNAME/inferplot.git
      cd inferplot

3. **Set Up Environment**: It's recommended to use `uv <https://docs.astral.sh/uv/>`_.

   .. code-block:: bash

      uv sync --all-extras
      uv pip install -e .
      uv run pre-commit install

Running Tests
-------------

We use `pytest` for testing. To run the tests, use the following command:

.. code-block:: bash

   uv run pytest

Submitting Changes
------------------

1. **Create a Branch**: Create a new branch for your changes.

   .. code-block:: bash

      git checkout -b your-branch-name

2. **Commit Your Changes**: Commit your changes with a clear and descriptive commit message.

   .. code-block:: bash

      git add .
      git commit -m "Your descriptive commit message"

3. **Push to Your Fork**: Push your changes to your forked repository.

   .. code-block:: bash

      git push origin your-branch-name

4. **Create a Pull Request**: Go to your `inferplot` repository on GitHub and create a pull request from your branch. Provide a detailed description of your changes.

Reporting Issues
----------------

If you find a bug or have a feature request, please open an issue on GitHub. Provide as much detail as possible, including steps to reproduce the issue.


Thank you for contributing to InferPlot!