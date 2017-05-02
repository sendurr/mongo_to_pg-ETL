FROM mongo:3.2
RUN apt-get update && apt-get install -y \
    bzip2 \
    curl \
  && rm -rf /var/lib/apt/lists/*

ENV DUMP_URI https://cdn.filestackcontent.com/JpmJwEWzSnqxx299Pwhy
ENV DUMP_DIR /tmp/db-dump
ENV DUMP_NAME practical-db.tar.gzip

RUN mkdir -p ${DUMP_DIR} \
  && curl -o ${DUMP_DIR}/${DUMP_NAME} -L ${DUMP_URI} \
  && tar -C ${DUMP_DIR} -zxf ${DUMP_DIR}/${DUMP_NAME}

COPY load-dump.sh /home
RUN chmod 777 /home/load-dump.sh
CMD /home/load-dump.sh