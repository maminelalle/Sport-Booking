import React from 'react';

const PrivateRoute = ({ children, requiredRole }) => {
  const auth = localStorage.getItem('access_token');

  if (!auth) {
    return <Navigate to="/login" />;
  }

  return children;
};

export default PrivateRoute;
