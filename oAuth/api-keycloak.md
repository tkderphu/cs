# Login

```
POST {keycloak-url}/realms/{realm-name}/protocol/openid-connect/token
```

```
curl -X POST \
  {keycloak-url}/realms/{realm-name}/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id={client-id}" \
  -d "client_secret={client-secret}" \   # only if confidential client
  -d "username={username}" \
  -d "password={password}" \
  -d "grant_type=password"
```