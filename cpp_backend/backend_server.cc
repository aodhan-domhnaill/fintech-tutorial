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
#include <cstdio>
#include <ctime>

#include <libpq-fe.h>

#include "absl/flags/flag.h"
#include "absl/flags/parse.h"
#include "absl/strings/str_format.h"

#include <grpcpp/ext/proto_server_reflection_plugin.h>
#include <grpcpp/grpcpp.h>
#include <grpcpp/health_check_service_interface.h>

#include "backend.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using ::Pricing;
using ::Stock;
using ::AvgPrice;
using google::protobuf::Empty;
using google::protobuf::Timestamp;

ABSL_FLAG(uint16_t, port, 50051, "Server port for the service");


// Logic and data behind the server's behavior.
class PricingServiceImpl final : public Pricing::Service {
  public:
    PGconn *conn; //postgres connection

  PricingServiceImpl() {
    const char *conn = std::getenv("POSTGRES_URI");
    std::cout << "Connecting to " << conn << std::endl;
    this->conn = PQconnectdb(conn);
    if (PQstatus(this->conn) != CONNECTION_OK) {
      std::cerr << "Failed connection" << std::endl;
    }

    
  }

  Status SavePrice(ServerContext* context, const Stock* request,
                   Stock* response) override {
    response->set_symbol(request->symbol());


    const char *query =  "INSERT INTO stock (_time, price, symbol) VALUES ($1, $2, $3)";

    // Submit the query and retrieve the result
    std::vector<const char*> paramValues;
    std::vector<int> paramLengths;
    std::vector<int> paramFormats;
    Timestamp t = request->timestamp();
    time_t ms = t.nanos()/1000;
    char buffer;

    strftime(&buffer, 26, "%Y-%m-%d %H:%M:%S", gmtime(&ms));
    std::cout << t.nanos() << std::endl;
    std::cout << "Created timestamp." << std::endl;

    paramValues.push_back(&buffer);
    paramLengths.push_back(26);
    paramFormats.push_back(0);
    std::cout << "Timestamp successfully pushed back." << std::endl;
    
    const float price = request->price();
    std::cout << "Created price." << std::endl;
    paramValues.push_back(std::to_string(price).c_str());
    paramLengths.push_back(std::to_string(price).length());
    paramFormats.push_back(0);
    
    std::cout << "price successfully pushed back." << std::endl;
    const char *sym = request->symbol().c_str();
    std::cout << "Created symbol." << std::endl;
    paramValues.push_back(sym);
    paramLengths.push_back(request->symbol().length());
    paramFormats.push_back(0);
    std::cout << "Symbol successfully pushed back." << std::endl;

    paramValues[0] = "2023-08-01 12:00:00";
    for (int i = 0; i < 3; i++) {
      std::cout << paramValues[i] << std::endl;
    }

    PGresult *res = PQexecParams(this->conn, query, 3, NULL, paramValues.data(), paramLengths.data(), paramFormats.data(), 0);
    std::cout << "Successfully executed query." << std::endl;
    // Check the status of the query result
    ExecStatusType resStatus = PQresultStatus(res);

    // Convert the status to a string and print it
    printf("Query Status: %s\n", PQresStatus(resStatus));

    // Check if the query execution was successful
    if (resStatus != PGRES_COMMAND_OK) {
        // If not successful, print the error message and finish the connection
        printf("Error while executing the query: %s\n", PQerrorMessage(this->conn));

        // Clear the result
        PQclear(res);

        switch (resStatus) {
          case PGRES_BAD_RESPONSE: 
            return Status::OK;
          case PGRES_FATAL_ERROR: 
            exit(1);
            return Status::OK;
          case PGRES_NONFATAL_ERROR: 
            return Status::OK;
          default: 
            return Status::OK;
        }

    }


    return Status::OK;
  }
  Status GetLatestPrice(ServerContext* context, const Empty* request,
                        Stock* response) override {
    char *query = "SELECT _time, price, symbol FROM stock LIMIT 1";

    // Submit the query and retrieve the result
    PGresult *res = PQexec(this->conn, query);

    // Check the status of the query result
    ExecStatusType resStatus = PQresultStatus(res);

    // Convert the status to a string and print it
    printf("Query Status: %s\n", PQresStatus(resStatus));

    // Check if the query execution was successful
    if (resStatus != PGRES_TUPLES_OK) {
        // If not successful, print the error message and finish the connection
        printf("Error while executing the query: %s\n", PQerrorMessage(this->conn));

        // Clear the result
        PQclear(res);

        switch (resStatus) {
          case PGRES_BAD_RESPONSE: 
            return Status::OK;
          case PGRES_FATAL_ERROR: 
            exit(1);
            return Status::OK;
          case PGRES_NONFATAL_ERROR: 
            return Status::OK;
          default: 
            return Status::OK;
        }

    }

    // We have successfully executed the query
    std::cout << "Query Executed Successfully" << std::endl;

    // Get the number of rows and columns in the query result
    int rows = PQntuples(res);
    int cols = PQnfields(res);
    std::cout << "Number of rows: \n" << rows << std::endl;
    std::cout << "Number of columns: \n" << cols << std::endl;

    // Print the column names
    for (int i = 0; i < cols; i++) {
        std::cout <<"\t" << PQfname(res, i) << std::endl;
    }
    std::cout << "\n";

    // Print all the rows and columns
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            // Print the column value
            std::cout << "\t" << PQgetvalue(res, i, j) << std::endl;
        }
        std::cout << "\n";
    }

    std::srand(std::time(nullptr));
    response->set_symbol(PQgetvalue(res, 0, 2));
    double price;
    sscanf(PQgetvalue(res, 0, 1), "%lf", &price);
    response->set_price(price);
    std::cout << "Price symbol set." << std::endl;

    Timestamp *t = new Timestamp();
    tm ctime;
    strptime(PQgetvalue(res, 0, 0), "%Y-%m-%d %T", &ctime);
    std::cout << "Parsing timestamp." << std::endl;
    t->set_seconds(mktime(&ctime));
    response->set_allocated_timestamp(t);
    std::cout << "Timestamp set." << std::endl;

    return Status::OK;
  }
  Status GetMvgAvg(ServerContext* context, const Empty* request,
                   AvgPrice* response) override {
    char *query = "SELECT price FROM mvg_avg LIMIT 1";

    // Submit the query and retrieve the result
    PGresult *res = PQexec(this->conn, query);

    // Check the status of the query result
    ExecStatusType resStatus = PQresultStatus(res);

    // Check if the query execution was successful
    if (resStatus != PGRES_TUPLES_OK) {
        // If not successful, print the error message and finish the connection
        printf("Error while executing the query: %s\n", PQerrorMessage(this->conn));

        // Clear the result
        PQclear(res);

        switch (resStatus) {
          case PGRES_BAD_RESPONSE: 
            return Status::OK;
          case PGRES_FATAL_ERROR: 
            exit(1);
            return Status::OK;
          case PGRES_NONFATAL_ERROR: 
            return Status::OK;
          default: 
            return Status::OK;
        }

    }


    // Get the number of rows and columns in the query result
    int rows = PQntuples(res);
    int cols = PQnfields(res);
    std::cout << "Number of rows: \n" << rows << std::endl;
    std::cout << "Number of columns: \n" << cols << std::endl;

    // Print the column names
    for (int i = 0; i < cols; i++) {
        std::cout <<"\t" << PQfname(res, i) << std::endl;
    }
    std::cout << "\n";

    // Print all the rows and columns
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            // Print the column value
            std::cout << "\t" << PQgetvalue(res, i, j) << std::endl;
        }
        std::cout << "\n";
    }

    double price;
    sscanf(PQgetvalue(res, 0, 0), "%lf", &price);
    response->set_price(price);
    std::cout << "Price symbol set." << std::endl;

    return Status::OK;
  }

  virtual ~PricingServiceImpl() { 
    PQfinish(this->conn); 
    };
};

/*
Pricing::Service::~Service() {
}

::grpc::Status Pricing::Service::SavePrice(::grpc::ServerContext* context, const ::::Stock* request, ::::Stock* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status Pricing::Service::GetLatestPrice(::grpc::ServerContext* context, const ::google::protobuf::Empty* request, ::::Stock* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status Pricing::Service::GetMvgAvg(::grpc::ServerContext* context, const ::google::protobuf::Empty* request, ::::AvgPrice* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}


*/

void RunServer(uint16_t port) {
  std::string server_address = absl::StrFormat("0.0.0.0:%d", port);
  PricingServiceImpl service;

  grpc::EnableDefaultHealthCheckService(true);
  grpc::reflection::InitProtoReflectionServerBuilderPlugin();
  ServerBuilder builder;
  // Listen on the given address without any authentication mechanism.
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  // Register "service" as the instance through which we'll communicate with
  // clients. In this case it corresponds to an *synchronous* service.
  builder.RegisterService(&service);
  // Finally assemble the server.
  std::unique_ptr<Server> server(builder.BuildAndStart());
  std::cout << "Server listening on " << server_address << std::endl;

  // Wait for the server to shutdown. Note that some other thread must be
  // responsible for shutting down the server for this call to ever return.
  server->Wait();
}

int main(int argc, char** argv) {
  absl::ParseCommandLine(argc, argv);
  RunServer(absl::GetFlag(FLAGS_port));
  return 0;
}
