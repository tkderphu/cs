# This is note about search job example about keycloak

In this example i will use frontend using ReactJS and backend using NodeJS

# Resources

1. CV management: Client have applied job and then is sent to company

2. Recruit management: Company posts job position

# Roles

1. Admin (Administrator of system)

2. Company (A representative company)

3. HR (a employee of company)

4. User (normal user)

# Permissions

1. Admin can control all resources

2. Company only control their resources such as CV, employee, create employee, delete emploee but only in that company

3. HR only control about post recruit, accept/reject CV

4. Only apply job

# Fake data

```
const companies = [
    {
        id: 1,
        name: "Cong ty TNHH 1"
    },
    {
        id: 2,
        name: "Cong ty TNHH 2"
    },
    {
        id: 3,
        name: "Cong ty TNHH 3"
    }
]

const posts = [
    {
        id: 1,
        name: "Recruit intern Java",
        company: 1
    },
    {
        id: 2,
        name: "Recruit intern C#",
        company: 2
    },
    {
        id: 3,
        name: "Recruit intern Python",
        company: 3
    }
]



const applied = [
    {
        id: 1,
        userId: 1,
        postId: 1
    }
]
```

# Dependencies for frontend

```
npm install keycloak-js @react-keycloak/web
```

- keycloak-js: The official JS adapter

- @react-keycloak/web: A React wrapper for easier integration (optional but recommended)

# Structure Source Code

```
src/
├── keycloak.js         # Keycloak config and init
├── App.js              # Main app
└── index.js            # Entry point
```

# Setup Keycloak in keycloak.js

```
// src/keycloak.js
import Keycloak from 'keycloak-js';

const keycloak = new Keycloak({
  url: 'http://localhost:8080/auth', // or /realms if newer version
  realm: 'your-realm-name',
  clientId: 'your-client-id',
});

export default keycloak;
```


# Setup keycloak provider in index.js

```
// src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { ReactKeycloakProvider } from '@react-keycloak/web';
import keycloak from './keycloak';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <ReactKeycloakProvider
    authClient={keycloak}
    initOptions={{ onLoad: 'login-required' }} // or 'check-sso'
  >
    <App />
  </ReactKeycloakProvider>
);
```

| Option             | Meaning                                                       |
| ------------------ | ------------------------------------------------------------- |
| `'login-required'` | Immediately redirect to Keycloak login if not authenticated   |
| `'check-sso'`      | Silently check if the user is already logged in (no redirect) |


# Use Authentication in App.js

```
// src/App.js
import React from 'react';
import { useKeycloak } from '@react-keycloak/web';

function App() {
  const { keycloak, initialized } = useKeycloak();

  if (!initialized) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Welcome to the React App</h1>
      {keycloak?.authenticated ? (
        <>
          <p>Logged in as: {keycloak.tokenParsed?.preferred_username}</p>
          <button onClick={() => keycloak.logout()}>Logout</button>
        </>
      ) : (
        <button onClick={() => keycloak.login()}>Login</button>
      )}
    </div>
  );
}

export default App;
```

<a>Link example</a>
