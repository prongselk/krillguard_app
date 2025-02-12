run_app:
    bash -c 'source /usr/share/miniconda/etc/profile.d/conda.sh && \
    conda activate myenv && \
    gunicorn --bind 0.0.0.0:8050 app:server & sleep 5 && \
    while ! nc -z 127.0.0.1 8050; do sleep 1; done'

	sleep 10

	wget -r http://127.0.0.1:8050/
	wget -r http://127.0.0.1:8050/_dash-layout 
	wget -r http://127.0.0.1:8050/_dash-dependencies

	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-graph.js
	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-highlight.js
	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-markdown.js
	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-datepicker.js

	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dash_table/async-table.js
	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dash_table/async-highlight.js

	wget -r http://127.0.0.1:8050/_dash-component-suites/plotly/package_data/plotly.min.js

	mv 127.0.0.1:8050 pages_files
	ls -a pages_files
#ls -a pages_files/assets

	find pages_files -exec sed -i.bak 's|_dash-component-suites|krillguard-app\\/_dash-component-suites|g' {} \;
	find pages_files -exec sed -i.bak 's|_dash-layout|krillguard-app/_dash-layout.json|g' {} \;
	find pages_files -exec sed -i.bak 's|_dash-dependencies|krillguard-app/_dash-dependencies.json|g' {} \;
	find pages_files -exec sed -i.bak 's|_reload-hash|krillguard-app/_reload-hash|g' {} \;
	find pages_files -exec sed -i.bak 's|_dash-update-component|krillguard-app/_dash-update-component|g' {} \;
#find pages_files -exec sed -i.bak 's|assets|krillguard-app/assets|g' {} \;

	mv pages_files/_dash-layout pages_files/_dash-layout.json
	mv pages_files/_dash-dependencies pages_files/_dash-dependencies.json
#mv assets/* pages_files/assets/

	ps -C python -o pid= | xargs kill -9

clean_dirs:
	ls
	rm -rf 127.0.0.1:8050/
	rm -rf pages_files/
	rm -rf joblib