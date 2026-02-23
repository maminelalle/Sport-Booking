import { useAuth } from '../context/AuthContext';

export const useAuthUser = () => {
  return useAuth();
};

export const useIsAuthenticated = () => {
  const { user } = useAuth();
  return !!user;
};

export const useIsAdmin = () => {
  const { user } = useAuth();
  return user?.role_name === 'ADMIN';
};

export const useIsManager = () => {
  const { user } = useAuth();
  return user?.role_name === 'Gestionnaire';
};

export const useIsClient = () => {
  const { user } = useAuth();
  return user?.role_name === 'CLIENT';
};
