/*
 *
 * Copyright 2015 gRPC authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

#include <iostream>
#include <memory>
#include <string>
#include<chrono>
#include<thread>

#include "absl/flags/flag.h"
#include "absl/flags/parse.h"

#include <grpcpp/grpcpp.h>

#ifdef BAZEL_BUILD
#include "examples/protos/helloworld.grpc.pb.h"
#else
#include "backend.grpc.pb.h"
#endif

ABSL_FLAG(std::string, target, "backend:50051", "Server address");

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using ::Pricing;
using ::Stock;
using ::AvgPrice;
using google::protobuf::Empty;
using google::protobuf::Timestamp;


int main(int argc, char** argv) {
  absl::ParseCommandLine(argc, argv);
  // Instantiate the client. It requires a channel, out of which the actual RPCs
  // are created. This channel models a connection to an endpoint specified by
  // the argument "--target=" which is the only expected argument.
  std::string target_str = absl::GetFlag(FLAGS_target);
  // We indicate that the channel isn't authenticated (use of
  // InsecureChannelCredentials()).
  std::shared_ptr<Channel> channel = grpc::CreateChannel(target_str, grpc::InsecureChannelCredentials());
  std::unique_ptr<Pricing::Stub> stub_ = Pricing::NewStub(channel);

  Empty empty = Empty();
  Stock request;
  Stock reply;
  ClientContext context;
  std::srand(std::time(nullptr));
  Timestamp t = Timestamp();
  //std::time_t currentTime;
  

  while (true) {
        stub_->GetLatestPrice(&context, empty, &reply);
        double old_price = reply.price();
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
        double new_price = (static_cast<double>(std::rand())/RAND_MAX)*200 - 100 + old_price;
        std::cout << "New Price is random: " << new_price << std::endl;
        request.set_symbol("CPPRAND");
        request.set_price(new_price);
        t.set_seconds(std::time(NULL));
        request.set_timestamp(&t);
        stub_->SavePrice(&context, request, &reply);
  }

  return 0;
}
