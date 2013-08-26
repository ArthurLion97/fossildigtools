CREATE TABLE "features" ("pkuid" integer primary key autoincrement, "number" integer NOT NULL, "identify" text , "fragment" integer , "origin" integer NOT NULL DEFAULT -1 , "grid" text , "block_id" text , "left_right" text , "associated" integer , "with_bone" integer , "counts" integer , "ontogeny" text , "genus" text , "percent" integer , "preservation" text , "packaging" text , "units" text NOT NULL, "length" real , "width" real , "breadth" real , "added" text NOT NULL, "geometry" MULTIPOLYGON);

INSERT INTO "features" ;

CREATE TABLE "aoi"(pkuid integer primary key autoincrement,"ftype" text, "geometry" POLYGON)


CREATE TABLE failed_banks_id (id integer primary key autoincrement, name text, city text, state text, zip integer, acquired_by text, close_date date, updated_date date);
INSERT INTO failed_banks_id(name, city, state, zip, acquired_by,close_date, updated_date) SELECT * FROM failed_banks;
