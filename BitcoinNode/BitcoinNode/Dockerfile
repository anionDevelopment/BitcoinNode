ARG image_debian
FROM ${image_debian}
ARG CodeUnitVersion
ARG bitcoin_version
# Set automatically by "docker buildx build --platform ..." (for example "amd64" or "arm64").
ARG TARGETARCH
LABEL version=${CodeUnitVersion}
ENV ISRUNNINGINCONTAINER="true"

LABEL description="BitcoinNode is a docker-image for simply running a bitcoin-node in a docker-container."

RUN mkdir /Workspace && \
    mkdir /Workspace/Program && \
    mkdir /Workspace/Data && \
    mkdir /Workspace/Temp && \
    mkdir /Workspace/Logs
WORKDIR /Workspace/Temp
COPY ./Other/Resources/Bitcoin/Bitcoin_${TARGETARCH}.tar.gz /Workspace/Temp/Bitcoin.tar.gz
RUN tar xzf Bitcoin.tar.gz && \
    install -m 0755 -o root -g root -t /usr/local/bin bitcoin-$bitcoin_version/bin/* && \
    cd / && \
    rm -rf /Workspace/Temp
COPY ./BitcoinNode/EntryPointScript.sh /Workspace/Program/EntryPointScript.sh
RUN chmod +x /Workspace/Program/EntryPointScript.sh
WORKDIR /Workspace/Program
ENTRYPOINT ["/Workspace/Program/EntryPointScript.sh"]
