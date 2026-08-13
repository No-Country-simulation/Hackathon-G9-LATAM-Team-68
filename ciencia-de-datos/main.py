from fastapi import FastAPI, HTTPException
import motor


app = FastAPI()


@app.post("/analizar")
def analizar(datos: dict):
    try:
        resultado = motor.funcion_integradora_final(datos)
        return resultado

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )