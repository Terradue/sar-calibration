$graph:
- baseCommand: sar-calibration
  hints:
    DockerRequirement:
      dockerPull: docker.terradue.com/sar_calibration:0.1
  class: CommandLineTool
  id: clt
  inputs:
    inp1:
      inputBinding:
        position: 1
        prefix: --input_references
      type: Directory
    inp2:
      inputBinding:
        position: 2
        prefix: --aoi
      type: string
  outputs:
    results:
      outputBinding:
        glob: .
      type: Directory
  requirements:
    EnvVarRequirement:
      envDef:
        PATH: /opt/anaconda/envs/env_sar_calibration/bin:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/envs/notebook/bin:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/condabin:/opt/anaconda/bin:/usr/lib64/qt-3.3/bin:/usr/share/java/maven/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
        PREFIX: /opt/anaconda/envs/sar_calibration
    ResourceRequirement: {}
  stderr: std.err
  stdout: std.out
- class: Workflow
  doc: SAR calibration processor
  id: sar-calibration
  inputs:
    aoi:
      doc: Area of interest in WKT
      label: Area of interest
      type: string
    input_reference:
      doc: EO product for vegetation index
      label: EO product for vegetation index
      type: Directory[]
  label: SAR calibration
  outputs:
  - id: wf_outputs
    outputSource:
    - node_1/results
    type:
      Directory
  steps:
    node_1:
      in:
        inp1: input_references
        inp2: aoi
      out:
      - results
      run: '#clt'
cwlVersion: v1.0
