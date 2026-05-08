{% macro offset_power(y0, a, alpha, period_col) %}

(
    {{ y0 }}
    + {{ a }} * POWER(
        {{ period_col }} - MIN({{ period_col }}) OVER () + 1,
        {{ alpha }}
    )
)

{% endmacro %}



{% macro bounded_power(u1, u2, tau1, tau2, alpha, x_col) %}

(
    {{ u1 }}
    + (
        (
            ({{ u2 }} - {{ u1 }})
            / POWER(({{ tau2 }} - {{ tau1 }}), {{ alpha }})
        )
        * POWER({{ x_col }} - {{ tau1 }}, {{ alpha }})
    )
)

{% endmacro %}



{% macro inverse_power(y1, x1, x_col, alpha) %}

(
    {{ y1 }} * POWER(
        {{ x1 }} / {{ x_col }},
        {{ alpha }}
    )
)

{% endmacro %}
