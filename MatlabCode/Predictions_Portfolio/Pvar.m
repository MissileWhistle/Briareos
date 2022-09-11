function v=Pvar(X,CovP)
  % X is a (1,n) vector
  v=sqrt(X*CovP*X');
end