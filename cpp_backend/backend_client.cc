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

#include "absl/flags/flag.h"
#include "absl/flags/parse.h"

#include <grpcpp/grpcpp.h>

#include "backend.grpc.pb.h"

ABSL_FLAG(std::string, target, "backend:50051", "Server address");

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using ::Pricing;
using ::Stock;
using ::AvgPrice;

class PricingClient {
 public:
  PricingClient(std::shared_ptr<Channel> channel)
      : stub_(Pricing::NewStub(channel)) {}

  // Assembles the client's payload, sends it and presents the response back
  // from the server.
  std::string SavePrice(const std::string& user) {
    // Data we are sending to the server.
    Stock request;
    request.set_symbol("CPP");

    // Container for the data we expect from the server.
    Stock reply;

    // Context for the client. It could be used to convey extra information to
    // the server and/or tweak certain RPC behaviors.
    ClientContext context;

    // The actual RPC.
    Status status = stub_->SavePrice(&context, request, &reply);

    // Act upon its status.
    if (status.ok()) {
      return reply.symbol();
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return "RPC failed";
    }
  }

 private:
  std::unique_ptr<Pricing::Stub> stub_;
};

int main(int argc, char** argv) {
  absl::ParseCommandLine(argc, argv);
  // Instantiate the client. It requires a channel, out of which the actual RPCs
  // are created. This channel models a connection to an endpoint specified by
  // the argument "--target=" which is the only expected argument.
  std::string target_str = absl::GetFlag(FLAGS_target);
  // We indicate that the channel isn't authenticated (use of
  // InsecureChannelCredentials()).
  PricingClient Pricing(
      grpc::CreateChannel(target_str, grpc::InsecureChannelCredentials()));
  std::string user("world");
  std::string reply = Pricing.SavePrice(user);
  std::cout << "Pricing received: " << reply << std::endl;

  return 0;
}
