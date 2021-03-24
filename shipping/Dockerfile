#
# Build
#
FROM debian:10 AS build

RUN apt-get update && apt-get -y install maven

WORKDIR /opt/shipping

COPY pom.xml /opt/shipping/
RUN mvn dependency:resolve
COPY src /opt/shipping/src/
RUN mvn package

#
# Run
#
FROM openjdk:8u92-jdk-alpine

EXPOSE 8080

WORKDIR /opt/shipping

ENV CART_ENDPOINT=cart:8080\
    DB_HOST=mysql\
    JAVA_TOOL_OPTIONS=""

COPY --from=build /opt/shipping/target/shipping-1.0.jar shipping.jar

CMD java $JAVA_TOOL_OPTIONS -jar shipping.jar

