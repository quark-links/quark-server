FROM openjdk:8-jre-alpine

WORKDIR /opt/
ADD ./target/vh7-*.jar vh7.jar

ENV SPRING_PROFILES_ACTIVE="production"
ENV VH7_MYSQL_HOST="127.0.0.1"
ENV VH7_MYSQL_PORT="3306"
ENV VH7_MYSQL_DATABASE="vh7"
ENV VH7_MYSQL_USERNAME="vh7-user"
ENV VH7_MYSQL_PASSWORD="password"
ENV VH7_SHORTURL_SALT="default_salt"

EXPOSE 8080

CMD ["java", "-jar", "/opt/vh7.jar"]