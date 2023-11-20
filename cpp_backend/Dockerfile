FROM ubuntu:23.04 as deps

RUN apt-get update \
    && apt-get install -y cmake build-essential autoconf libtool pkg-config git

ARG MY_INSTALL_DIR=/grpc/

WORKDIR /build/

RUN git clone --recurse-submodules \
        -b v1.58.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc

WORKDIR /build/grpc

RUN mkdir -p cmake/build
WORKDIR /build/grpc/cmake/build
RUN cmake -DgRPC_INSTALL=ON \
      -DgRPC_BUILD_TESTS=OFF \
      -DCMAKE_INSTALL_PREFIX=${MY_INSTALL_DIR} \
      ../..
RUN make -j 4
RUN make install

FROM ubuntu:23.04 as builder

RUN apt-get update \
    && apt-get install -y cmake build-essential autoconf libtool pkg-config git

COPY --from=deps /grpc/ /grpc/

WORKDIR /build/

COPY . .

RUN mkdir build \
    && cd build \
    && cmake .. -DCMAKE_PREFIX_PATH=/grpc/ \
    && make

FROM ubuntu:23.04 AS runner

COPY --from=builder /build/build/greeter_server /greeter_server

ENTRYPOINT [ "/greeter_server" ]