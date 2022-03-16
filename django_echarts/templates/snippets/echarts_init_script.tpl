{% if c.geojson %}
$.getJSON("{% url "dje_geojson" c.geojson.geojson_name %}").done(function(mapdata){
    echarts.registerMap("{{ c.geojson.map_name }}", mapdata);
{% endif %}
    var chart_{{ c.chart_id }} = echarts.init(
        document.getElementById('{{ c.chart_id }}'), '{{ c.theme }}', {renderer: '{{ c.renderer }}'});
    {% for js in c.js_functions.items %}
        {{ js|safe }}
    {% endfor %}
    var option_{{ c.chart_id }} = {{ c.dump_options|default:'{}'|safe }};
    chart_{{ c.chart_id }}.setOption(option_{{ c.chart_id }});
    {% if c.is_geo_chart %}
        var bmap = chart_{{ c.chart_id }}.getModel().getComponent('bmap').getBMap();
        {% if c.bmap_js_functions %}
            {% for fn in c.bmap_js_functions.items %}
                {{ fn|safe }}
            {% endfor %}
        {% endif %}
    {% endif %}

    window.addEventListener('resize', function(){
        chart_{{ c.chart_id }}.resize();
    });
{% if c.geojson %}
}).fail(function(jqXHR, textStatus, error){
    $("#{{ c.chart_id }}").html("Load fail! Status: " + textStatus);
});
{% endif %}