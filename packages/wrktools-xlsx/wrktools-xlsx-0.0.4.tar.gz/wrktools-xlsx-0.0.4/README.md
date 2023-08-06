[![Build status](https://robertoprevato.visualstudio.com/wrktoolbox/_apis/build/status/wrktoolbox-xlsx-CI)](https://robertoprevato.visualstudio.com/wrktoolbox/_build/latest?definitionId=20) [![pypi](https://img.shields.io/pypi/v/wrktools-xlsx.svg?color=blue)](https://pypi.org/project/wrktools-xlsx/) [![Test coverage](https://img.shields.io/azure-devops/coverage/robertoprevato/wrktoolbox/20.svg)](https://robertoprevato.visualstudio.com/wrktoolbox/_build?definitionId=20)

# wrktoolbox-xlsx
XLSX spreadsheet reports for [wrktoolbox](https://github.com/RobertoPrevato/wrktoolbox).

```bash
pip install wrktools-xlsx
```

## Example configuration

**YAML**
```yaml
# importers read benchmarks results
importers:
  - type: json
    root_folder: data/results

# reports generation supports plugins, like benchmarks logic
plugins:
  - wrktoolboxxlsx.xlsx

# writers write reports
writers:
  - type: xlsx
    file_name: example.xlsx

```

**JSON**
```yaml
{
  "importers": [
    {
      type: "json",
      root_folder: "data/results"
    }
  ],
  
  "plugins": ["wrktoolboxxlsx.xlsx"],
  
  "writers": [
    {
      type: "xlsx",
      file_name: "example.xlsx"
    }
  ],
}

```

## Usage
```bash
wrktoolbox reports --settings configuration.yaml
```