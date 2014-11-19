-- Base table structure , all varchar
CREATE TABLE data (unique_hash varchar(512), email varchar(256), code varchar(256), comments varchar(256));

-- New table definitions changed datatype of code and comments to 'text' to store larger data
CREATE TABLE data (unique_hash varchar(512), email varchar(256), code text, comments text);
