# Analizador de Operaciones de Concentración (Fusiones)

Herramienta para simular fusiones entre empresas y evaluar su impacto en la competencia usando el Índice de Herfindahl-Hirschman (IHI), que es la métrica que usa como referencia la Fiscalía Nacional Económica (FNE) para analizar operaciones de concentración en Chile.

La hice como proyecto para el curso de Derecho Económico II, básicamente para tener una forma más rápida y visual de aplicar la teoría de concentración de mercado a casos concretos, en lugar de hacer los cálculos a mano.

## Qué hace

- Permite ingresar un mercado relevante y las participaciones de las empresas que compiten en él.
- Simula la fusión entre dos de esas empresas.
- Calcula el IHI antes y después de la fusión, y el ΔIHI (la variación que aporta específicamente la operación).
- Según esos números, clasifica el riesgo de la operación (bajo, moderado o alto) y entrega un dictamen preliminar con la justificación.
- Muestra gráficos de torta comparando la estructura del mercado antes y después.

## La metodología, en corto

El IHI es la suma de los cuadrados de las participaciones de mercado (en %), en una escala de 0 a 10.000:

```
IHI = Σ (participación_i)²
```

Cuando se fusionan dos empresas con participaciones s1 y s2, el aporte marginal al IHI es exactamente:

```
ΔIHI = 2 × s1 × s2
```

Los umbrales que usé para clasificar el riesgo (basados en los estándares de referencia comparados, FNE / Horizontal Merger Guidelines):

| IHI post-fusión | ΔIHI | Calificación |
|---|---|---|
| Menor a 1.500 | - | Baja concentración, riesgo bajo |
| Entre 1.500 y 2.500 | Menor a 250 | Concentración media, riesgo moderado-bajo |
| Entre 1.500 y 2.500 | 250 o más | Concentración media, riesgo moderado-alto |
| Mayor a 2.500 | Menor a 150 | Alta concentración, pero riesgo bajo (es preexistente) |
| Mayor a 2.500 | 150 o más | Alta concentración, alerta de alto riesgo |

## Cómo correrlo

Necesitas Python 3.9 o superior.

```bash
git clone https://github.com/TU_USUARIO/analizador-fusiones.git
cd analizador-fusiones
pip install -r requirements.txt
streamlit run analizador_fusiones.py
```

Se abre en el navegador, en localhost:8501.

## Uso

1. En el panel lateral, ingresa el mercado relevante y la lista de empresas con su participación, separadas por comas. Por ejemplo:

   ```
   Empresa A: 40, Empresa B: 30, Empresa C: 20, Empresa D: 10
   ```

2. Click en "Cargar / Actualizar Datos".
3. Elige las dos empresas que se van a fusionar.
4. Click en "Simular Fusión" y ahí salen los resultados, los gráficos y el dictamen.

## Estructura

```
.
├── analizador_fusiones.py   -> la app
├── requirements.txt         -> dependencias
└── README.md
```

## Una aclaración

Esto es una herramienta para fines de estudio, no un informe legal. No reemplaza el análisis completo que hace la FNE en un caso real (que considera muchas más variables además del IHI: barreras de entrada, poder de compra, rivalidad dinámica, etc). Los umbrales que usé son los estándares de referencia más comunes, pero en un caso real hay que revisar la Guía vigente de la FNE.

## Autor

Renato Vicencio
Estudiante de Derecho, 2do año - Pontificia Universidad Católica de Chile
