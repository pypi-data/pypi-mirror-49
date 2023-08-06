# What's that thing?

Ce repo contient le code d'un opérateur k8s qui reconfigure un load balancer
externe au cluster (*e.g* un HAProxy) en réaction au actions sur les services
de type loadBalancer, c'est à dire les créations, mises à jour, suppressions.

Cet opérateur n'est pas déployé dans le cluster k8s mais doit être déployé sur
les machines HAProxy.

Il permet d'adresser 3 scénarios :
  - HAProxy + keepalived
  - Envoy + keepalived
  - keepalived only

# TODO

- Le code de déploiement de l'application.
  - l'unité systemd
  - le templating de la configuration
