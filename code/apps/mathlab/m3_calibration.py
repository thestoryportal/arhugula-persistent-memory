# /// script
# requires-python = ">=3.11"
# dependencies = ["marimo", "duckdb", "pydantic", "psutil", "numpy", "torch==2.8.0"]
# ///
import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))
    import marimo as mo
    from pydantic import BaseModel, ConfigDict, Field
    from apps.mathlab import core
    from apps.mathlab import mathlab_runtime as runtime

    class Params(BaseModel):
        model_config = ConfigDict(extra="forbid")
        harvest_dir: Path = Field(description="Frozen operand harvest directory")
        reproduction_dir: Path = Field(description="Step 2 directory with passing exact replay")
        output_root: Path = Field(default=runtime.ROOT / runtime.L.ML_RUNS, description="Fresh result directories; fixtures use staging")
        index_path: Path = Field(default=runtime.ROOT / "experiments/ml/runs/calibration/calibration.duckdb", description="Derived, rebuildable citation index")

    return Params, core, json, mo


@app.cell
def _(Params, mo):
    form = mo.ui.dictionary({"harvest_dir": mo.ui.text(label="Harvest directory"),
                             "reproduction_dir": mo.ui.text(label="Passing step 2 directory"),
                             "output_root": mo.ui.text(value=str(Params.model_fields["output_root"].default), label="Output parent"),
                             "index_path": mo.ui.text(value=str(Params.model_fields["index_path"].default), label="Derived index")}).form()
    form
    return (form,)


@app.cell
def _(Params, form, mo):
    script_mode = mo.app_meta().mode == "script"
    cli = {k.replace("-", "_"): v for k, v in mo.cli_args().items()}
    mo.stop(not script_mode and form.value is None, mo.md("Choose the harvest and its passing replay, then submit."))
    params = Params(**(cli if script_mode else form.value))
    return (params,)


@app.cell
def _(core, json, mo, params):
    result = core.run_notebook(3, params)
    print(json.dumps(result, indent=2, allow_nan=False))
    mo.md(f"**MATH-PROXY** · Retrospective tier discrimination: **{result['outcome']}**. "
          "FAIL stops the lab cheaply. INVALID has no verdict. Prospective queue utility remains UNVERIFIED.")
    return (result,)


if __name__ == "__main__":
    app.run()
