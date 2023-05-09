# ITS PROJEKT 1

- **Autor:** Daniel Fajmon (xfajmo05)
- **Datum:** 2023-03-15

## Vyhledávání a nákup zboží (purchase.feature)
----------------------------------------------------
Testuje vyhledávání produktů, přidávání do koše, odebrání z koše a potvrzení objednávky.

## Registrace a historie nákupů (registration.feature)
----------------------------------------------------
Testuje vytváření uživatele a zobrazení historie nákupů se statusem objednávky.

## Správa zboží a jeho skladovosti (manage_items.feature)
----------------------------------------------------
Testuje vyhledávání zboží, odstranění, přidání, filtrování podle ceny, uprávy dostupného počtu u produktu.

## Správa objednávek (manage_orders.feature)
----------------------------------------------------
Testuje viditelnost objednávky, upravení statusu, odstranění a vytvoření objednávky.

## Správa zákaznických účtů (manage_customers.feature)
----------------------------------------------------
Testuje vytváření zákazníka, odstranění, změna hesla a úpravu adresy zákazníka.

## Matice pokrytí artefaktů

| Feature index                 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|-------------------------------|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|----|----|----|----|----|----|
| Page Index                    | x | x | x |   |   |   |   |   |   |    |    |    |    |    |    |    |    |    |    |    |    |
| Page Shopping cart            |   |   |   | x |   |   |   |   |   |    |    |    |    |    |    |    |    |    |    |    |    |
| Page Checkout                 |   |   |   |   | x |   |   |   |   |    |    |    |    |    |    |    |    |    |    |    |    |
| Page Registration             |   |   |   |   |   | x |   |   |   |    |    |    |    |    |    |    |    |    |    |    |    |
| Page My account               |   |   |   |   |   |   | x |   |   |    |    |    |    |    |    |    |    |    |    |    |    |
| Page Administration/Catalog   |   |   |   |   |   |   |   | x | x | x  | x  | x  | x  |    |    |    |    |    |    |    |    |
| Page Administration/Orders    |   |   |   |   |   |   |   |   |   |    |    |    |    | x  | x  | x  | x  |    |    |    |    |
| Page Administration/Customers |   |   |   |   |   |   |   |   |   |    |    |    |    |    |    |    |    | x  | x  | x  | x  |

## Matice pokrytí aktivit

| Activities                    | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|-------------------------------|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|----|----|----|----|----|----|
| Putting XYZ to cart           |   | x | x |   |   |   |   |   |   |    |    |    |    |    |    |    |    |    |    |    |    |
| Searching XYZ ...             | x |   | x |   |   |   |   | x |   |    | x  | x  | x  |    |    |    |    |    |    |    |    |
| Checking out                  |   |   |   |   | x |   |   |   |   |    |    |    |    |    |    |    |    |    |    |    |    |
| Registering ...               |   |   |   |   |   | x |   |   |   |    |    |    |    |    |    |    |    |    |    |    |    |
| Creating XYZ ...              |   |   |   |   |   |   |   |   |   | x  |    |    |    |    |    |    | x  | x  |    |    |    |
| Removing ...                  |   |   |   | x |   |   |   |   | x |    |    |    |    |    |    | x  |    |    | x  |    |    |
| Update ...                    |   |   |   |   |   |   |   |   |   |    |    |    | x  |    | x  |    |    |    |    | x  | x  |
| Show XYZ ...                  |   |   |   |   |   |   | x |   |   |    |    |    |    | x  |    |    |    |    |    |    |    |

## Matice Feature-Test

| Feature file             | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|--------------------------|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|----|----|----|----|----|----|
| purchase.feature         | x | x | x | x | x |   |   |   |   |    |    |    |    |    |    |    |    |    |    |    |    |
| registration.feature     |   |   |   |   |   | x | x |   |   |    |    |    |    |    |    |    |    |    |    |    |    |
| manage_items.feature     |   |   |   |   |   |   |   | x | x | x  | x  | x  | x  |    |    |    |    |    |    |    |    |
| manage_orders.feature    |   |   |   |   |   |   |   |   |   |    |    |    |    | x  | x  | x  | x  |    |    |    |    |
| manage_customers.feature |   |   |   |   |   |   |   |   |   |    |    |    |    |    |    |    |    | x  | x  | x  | x  |
