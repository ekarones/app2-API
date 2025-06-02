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
('Pudrición Negra', 'La pudrición negra es una enfermedad causada por el hongo Botryosphaeria obtusa. Afecta las hojas, frutos y ramas del manzano, causando manchas oscuras que eventualmente se convierten en lesiones circulares. En los frutos, la enfermedad provoca pudrición y manchas negras características.','Black rot.jpg'),
('Saludable', 'El estado saludable indica que la hoja del manzano no muestra signos de enfermedades o infecciones visibles. Las hojas tienen un color verde uniforme y están libres de manchas o daños causados por patógenos.','Healthy.jpg'),
('Roya del Cedro y Manzano', 'La roya del cedro y manzano es una enfermedad fúngica causada por el hongo Gymnosporangium juniperi-virginianae. Aparece como manchas amarillas o anaranjadas en las hojas, y afecta tanto a manzanos como a cedros. Si no se controla, puede causar defoliación severa.','Cedar rust.jpg'),
('Sarna del Manzano', 'La sarna del manzano es una enfermedad causada por el hongo Venturia inaequalis. Produce manchas oscuras en las hojas y frutos, y si la infección es severa, puede provocar deformidades en el fruto y la caída de hojas.','Scab.jpg'),
('Oidio', 'El oídio es una enfermedad fúngica causada por el hongo Podosphaera leucotricha, que afecta principalmente las hojas, brotes y frutos del manzano. Se manifiesta como un polvo blanco o grisáceo en la superficie de las hojas y otras partes jóvenes de la planta. Esta enfermedad debilita el árbol, reduce la fotosíntesis y puede deformar los frutos, disminuyendo su calidad y valor comercial.', 'Powdery mildew.jpg'),
('Arañita Roja', 'La arañita roja (Tetranychus urticae) es una plaga común en los manzanos, especialmente en climas cálidos y secos. Estos ácaros se alimentan de la savia de las hojas, provocando manchas amarillas, debilitamiento del árbol y reducción en la calidad y cantidad del fruto. Una infestación severa puede causar la caída prematura de las hojas y afectar el desarrollo de las manzanas.', 'Red spider mite.jpg');

INSERT INTO "advices" ("disease_name", "description") 
VALUES
('Pudrición Negra', 'Elimina y destruye las ramas, frutos y hojas infectadas para evitar la propagación del hongo.'),
('Pudrición Negra', 'Aplica fungicidas específicos a principios de la temporada de crecimiento para reducir la infección.'),
('Pudrición Negra', 'Asegura una buena circulación de aire mediante poda adecuada y evita el exceso de humedad en el follaje.'),

('Roya del Cedro y Manzano', 'Elimina los hospedadores alternativos como los cedros cercanos para interrumpir el ciclo de vida del hongo.'),
('Roya del Cedro y Manzano', 'Aplica fungicidas preventivos en primavera para proteger las hojas jóvenes del manzano.'),
('Roya del Cedro y Manzano', 'Asegura una adecuada distancia entre los árboles para reducir la humedad y la propagación de esporas.'),

('Sarna del Manzano', 'Retira y destruye las hojas y frutos caídos para minimizar la fuente de infección.'),
('Sarna del Manzano', 'Utiliza variedades de manzano resistentes a la sarna para reducir la susceptibilidad a la enfermedad.'),
('Sarna del Manzano', 'Aplica tratamientos con fungicidas de manera preventiva en la primavera y durante períodos húmedos.'),

('Oidio', 'Poda y elimina las partes afectadas del árbol para reducir la propagación del hongo.'),
('Oidio', 'Evita el exceso de humedad y mejora la ventilación entre los árboles mediante poda regular.'),
('Oidio', 'Aplica fungicidas específicos para oídio al inicio de la brotación y repite según recomendación técnica.'),

('Arañita Roja', 'Monitorea regularmente el envés de las hojas para detectar la presencia de ácaros tempranamente.'),
('Arañita Roja', 'Promueve enemigos naturales como ácaros depredadores para un control biológico efectivo.'),
('Arañita Roja', 'Aplica acaricidas selectivos si la infestación es alta, siguiendo las dosis y tiempos recomendados.');

INSERT INTO "notifications" ("title", "description", "creation_date") VALUES ('Version 1.0.0', 'first version', DATETIME('now', 'localtime'));