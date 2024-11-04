FROM php:8-apache

ENV PORT 22000

RUN apt update -y && docker-php-ext-install mysqli && docker-php-ext-enable mysqli

COPY . /var/www/html/
RUN sed -i "s/80/$PORT/g" /etc/apache2/sites-available/000-default.conf /etc/apache2/ports.conf
