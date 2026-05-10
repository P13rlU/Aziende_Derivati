-- Crezione Utente
create user <nome_schema>
identified by <password>
default tablespace users
quota unlimited on users;

-- Permessi
grant create session to <nome_schema>
grant create table to <nome_schema>
grant create view to <nome_schema>
grant create sequence to <nome_schema>
grant create trigger to <nome_schema>
grant create procedure to <nome_schema>
