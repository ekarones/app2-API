DROP TABLE IF EXISTS "diseases";
DROP TABLE IF EXISTS "advices";
DROP TABLE IF EXISTS "users";
DROP TABLE IF EXISTS "records";
DROP TABLE IF EXISTS "admins";
DROP TABLE IF EXISTS "notifications";

CREATE TABLE "diseases" (
	"id"    INTEGER NOT NULL,
	"name"  TEXT NOT NULL,
	"description"   TEXT NOT NULL,
	"image_name" TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "advices" (
	"id"	INTEGER NOT NULL,
	"disease_name"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "users" (
	"id"	INTEGER NOT NULL,
	"username"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "admins" (
	"id"	INTEGER NOT NULL,
	"username"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "records" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"image_name"	TEXT NOT NULL,
	"disease_id"	INTEGER NOT NULL,
	"disease_name"	TEXT NOT NULL,
	"diagnosis_date"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "users"("id"),
	FOREIGN KEY("disease_id") REFERENCES "diseases"("id")
);

CREATE TABLE "notifications" (
	"id"	INTEGER NOT NULL,
	"title"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	"creation_date"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

INSERT INTO "admins" ("username", "email", "password") VALUES ('admin', 'admin@gmail.com', 'admin123');

INSERT INTO "users" ("username", "email", "password") VALUES ('Erick','erick19arones@gmail.com','erick123');

INSERT INTO "diseases" ("name", "description", "image_name") 
VALUES
('Black Rot (Pudrición Negra)', 'La pudrición negra es una enfermedad causada por el hongo Botryosphaeria obtusa. Afecta las hojas, frutos y ramas del manzano, causando manchas oscuras que eventualmente se convierten en lesiones circulares. En los frutos, la enfermedad provoca pudrición y manchas negras características.','Black rot.jpg'),
('Healthy (Saludable)', 'El estado saludable indica que la hoja del manzano no muestra signos de enfermedades o infecciones visibles. Las hojas tienen un color verde uniforme y están libres de manchas o daños causados por patógenos.','Healthy.jpg'),
('Cedar Rust (Roya del Cedro y Manzano)', 'La roya del cedro y manzano es una enfermedad fúngica causada por el hongo Gymnosporangium juniperi-virginianae. Aparece como manchas amarillas o anaranjadas en las hojas, y afecta tanto a manzanos como a cedros. Si no se controla, puede causar defoliación severa.','Cedar rust.jpg'),
('Scab (Sarna del Manzano)', 'La sarna del manzano es una enfermedad causada por el hongo Venturia inaequalis. Produce manchas oscuras en las hojas y frutos, y si la infección es severa, puede provocar deformidades en el fruto y la caída de hojas.','Scab.jpg');

INSERT INTO "advices" ("disease_name", "description") 
VALUES
('Black Rot (Pudrición Negra)', 'Elimina y destruye las ramas, frutos y hojas infectadas para evitar la propagación del hongo.'),
('Black Rot (Pudrición Negra)', 'Aplica fungicidas específicos a principios de la temporada de crecimiento para reducir la infección.'),
('Black Rot (Pudrición Negra)', 'Asegura una buena circulación de aire mediante poda adecuada y evita el exceso de humedad en el follaje.'),

('Cedar Rust (Roya del Cedro y Manzano)', 'Elimina los hospedadores alternativos como los cedros cercanos para interrumpir el ciclo de vida del hongo.'),
('Cedar Rust (Roya del Cedro y Manzano)', 'Aplica fungicidas preventivos en primavera para proteger las hojas jóvenes del manzano.'),
('Cedar Rust (Roya del Cedro y Manzano)', 'Asegura una adecuada distancia entre los árboles para reducir la humedad y la propagación de esporas.'),

('Scab (Sarna del Manzano)', 'Retira y destruye las hojas y frutos caídos para minimizar la fuente de infección.'),
('Scab (Sarna del Manzano)', 'Utiliza variedades de manzano resistentes a la sarna para reducir la susceptibilidad a la enfermedad.'),
('Scab (Sarna del Manzano)', 'Aplica tratamientos con fungicidas de manera preventiva en la primavera y durante períodos húmedos.');

INSERT INTO "notifications" ("title", "description", "creation_date") VALUES ('Version 1.0.0', 'first version', DATETIME('now', 'localtime'));