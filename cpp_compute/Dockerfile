FROM alpine:3.18 as deps

RUN apk add --no-cache git

WORKDIR /build/

RUN git clone --recurse-submodules \
        -b v1.58.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc

RUN apk add --no-cache cmake build-base autoconf libtool pkgconfig git linux-headers

ARG MY_INSTALL_DIR=/grpc/

WORKDIR /build/grpc

RUN mkdir -p cmake/build
WORKDIR /build/grpc/cmake/build
RUN cmake -DgRPC_INSTALL=ON \
      -DgRPC_BUILD_TESTS=OFF \
      -DCMAKE_INSTALL_PREFIX=${MY_INSTALL_DIR} \
      ../..
RUN make -j 4
RUN make install

FROM alpine:3.18 as builder

RUN apk add --no-cache cmake build-base autoconf libtool pkgconfig git linux-headers

COPY --from=deps /grpc/ /grpc/

WORKDIR /build/

COPY . .

RUN mkdir build \
    && cd build \
    && cmake .. -DCMAKE_PREFIX_PATH=/grpc/ \
    && make \
    || cat backend.grpc.pb.h >> /dev/stderr ;exit 1

FROM scratch AS client

COPY --from=builder /build/build/backend_client /backend_client

ENTRYPOINT [ "/backend_client" ]