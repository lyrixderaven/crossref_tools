FROM python:3.5
RUN apt-get update && apt-get install -y \
  gcc \
  gettext \
  postgresql-client libpq-dev \
  sqlite3 \
  --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/crossref_tools
WORKDIR /usr/src/crossref_tools

ADD requirements.txt /usr/src/crossref_tools/
RUN pip install --no-cache-dir -r requirements.txt
ADD README.txt CHANGES.txt MANIFEST.in setup.py /usr/src/crossref_tools/
RUN pip install -e . && pip install -e ".[testing]"
ADD development.ini /usr/src/crossref_tools/

ADD crossref_tools /usr/src/crossref_tools/crossref_tools
RUN initialize_crossref_tools_db development.ini

EXPOSE 6543
CMD pserve development.ini --reload