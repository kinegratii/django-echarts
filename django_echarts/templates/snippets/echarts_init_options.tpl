{% for custom_map_item, chart_list in structured_data %}
    {% if custom_map_item.url %}
$.get({
   url: '{{ custom_map_item.url }}',
   dataType: '{{ custom_map_item.ajax_data_type }}'
}).done(function(mapData){
    echarts.registerMap("{{ custom_map_item.map_name }}", {{ custom_map_item.param_str }});
    {% endif %}
    {% for c in chart_list %}
    var chart_{{ c.chart_id }} = echarts.init(
        document.getElementById('{{ c.chart_id }}'), '{{ c.dje_echarts_theme }}', {renderer: '{{ c.renderer }}'});
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
    {% endfor %}

    {% if custom_map_item.url %}
}).fail(function(jqXHR, textStatus, error){
    $("#{{ c.chart_id }}").html("Load custom map fail! Status: " + textStatus);
});
    {% endif %}
{% endfor %}