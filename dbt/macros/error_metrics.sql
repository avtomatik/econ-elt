{% macro error_metrics(actual, predicted) %}
    POWER({{ actual }} - {{ predicted }}, 2) AS squared_error
{% endmacro %}

{% macro msd(table) %}
    AVG(squared_error) AS msd,
    SQRT(AVG(squared_error)) AS rmsd
{% endmacro %}
