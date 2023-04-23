Nume: Nita Robert-Andrei
Grupă:344 C4

# Tema <1> Marketplace

Organizare


Am încercat să găsesc o soluție simplă și ușor de înțeles
pentru problema, care implică o listă cu produse disponibile
la un moment dat și care poate fi folosită de către 
consumatori și producători, numită "avb_products". 
Produsele sunt definite de clasa "Item" și sunt reprezentate
prin produs + id_producător.Pentru a contoriza numărul de produse 
afișate de fiecare producător, am utilizat un dicționar numit
"published_products_count". 
De asemenea, am creat un dicționar de "Item-uri" pentru coșuri.


Implementare

Am implementat toate cerințele din scheletul problemei și am trecut toate 
testele oferite de checker, fără a utiliza unittesting. De asemenea, 
am folosit metoda "converter" în loc de "formatTime" 
pentru a afișa timpul în logging. Mi s-a părut 
interesantă utilizarea decoratorilor în declarația claselor,
în special în cazul clasei "Product", și am aplicat această
metodă și pentru clasa "Item".



Resurse utilizate

https://ocw.cs.pub.ro/courses/asc/laboratoare/02
https://www.programcreek.com/python/example/1475/logging.handlers.RotatingFileHandler

Git

https://github.com/Raresul/Multi-Producer---Multi-Consumer-Marketplace