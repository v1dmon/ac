run:
	poetry run python ac.py cut -i ../data/trace/karthik.trace -t $(CUT) |\
	poetry run python ac.py zip -t $(ZIP) |\
	poetry run python ac.py gen -a ../data/apispec/sockshop.yml	|\
	bat -l yaml --paging never
