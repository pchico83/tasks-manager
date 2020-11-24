db:
	mongosh -u mongo -p secretpassword --tls --tlsCertificateKeyFile /etc/ca-clients/client-pem --tlsCAFile /etc/ca-clients/mongodb-ca-cert mongo-mongodb-headless/db 