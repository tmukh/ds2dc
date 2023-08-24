## Installation

To install DS2DCGen, follow these steps:

1. Clone the GitHub repository:
   ```
   git clone https://git.cs.uni-kl.de/g_donipart17/ds2dcgen.git
   ```

2. Change to the cloned directory:
   ```
   cd ds2dcgen/smartconvDS
   ```

3. Install the required dependencies using `pip` and the `requirements.txt` file:
   ```
   pip install -r requirements.txt
   ```

   This command will install all the necessary dependencies for DS2DCGen based on the versions specified in the `requirements.txt` file.

That's it! You have successfully installed DS2DCGen and its dependencies.

## Usage

To run DS2DCGen, execute the following command from the root folder:

```
py -m run_converter.py [Data model] [root folder]
```

DS2DCGen supports several command-line arguments to specify the conversion process. Here are the available options:

### Multimodel Conversion

```
py -m run_converter.py multimodel [root_folder]
```

- Description: Enables multimodel conversion and generates multiple data containers for the given data structure.
- Output: Generates a Docker Compose file with multiple containers, each representing a different data model.

### Same-Datamodel Conversion

```
py -m run_converter.py [format] [root_folder]
```

- Description: Performs the conversion of a data structure into a specific data container format.
- Parameters:
  - `[format]`: The target data container format. Valid options: tabular, graph, keyvalue, document.

### Domain-Specific Conversion (To be Implemented)

```
py -m run_converter.py domain-specific [root_folder]
```

- Description: Specifies a domain-specific conversion process. Please note that this feature is yet to be implemented.

**Note**: Ensure that you have the required dependencies and configurations in place before running DS2DCGen with different arguments.

## Contributing

Contributions to DS2DCGen are welcome! If you encounter any issues or have suggestions for improvement, please open an issue on the [GitHub repository](https://git.cs.uni-kl.de/g_donipart17/ds2dcgen/issues).

When contributing code, please follow the existing coding style and submit your pull requests. Your contributions will be reviewed by the project maintainers.

## License

DS2DCGen is distributed under the [MIT License](LICENSE). Feel free to use, modify, and distribute this software according to the terms of the license.

## Contact

For any inquiries or further information about DS2DCGen, you can contact:

- Tarik Abu Mukh
- Email: [abumukht@protonmail.com](mailto:abumukht@protonmail.com)

Feel free to reach out with any questions or feedback related to DS2DCGen.
