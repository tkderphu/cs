# Note use case diagram


## Usecase

Use cases are enclosed using between parentheses

Also use `usecase` keyword to define a usecase, to define an alias using `as` keyword.

```
@startuml

(first usecase)
(Another usecase) as (UC2)

usecase UC3
usecase (LAST\nusecase) as UC4

@enduml
```

## Actor

the name an actor is enclosed between colons, also use `actor` keyword.

```
:First Actor:
actor Woman3
```

## Use package

Use packages to group actors or use cases:

```
@startuml


actor Guest as g
package Professional {
    actor Chef as c
    actor "Food critic" as fc
}

package Restaurant {
    usecase "Eat food" as UC1
}

g -- UC1

@enduml
```

We can use `rectangle` to change the display of the package

## Extends

If one actor/use case extends another one use the symbol `<|--`

```
@startuml

actor Admin
actor "Use the application" as Use

User <|-- Admin
(Start) <|-- Use

@enduml
```

## Label

To add label to the link we use `:` after link

```
@startuml
actor "Customer" as customer
actor "Login" as login

customer --> login:"Customer must login"
@enduml
```


## Change direction Left to Right

top to bottom

```
@startuml
'default
top to bottom direction
user1 --> (Usecase 1)
user2 --> (Usecase 2)

@enduml
```

left to right

```
@startuml

left to right direction
user1 --> (Usecase 1)
user2 --> (Usecase 2)


left to right direction

actor "Customer" as customer
actor "Payment Gateway" as paymentGateway

usecase "Place Order" as placeOrder
usecase "Process Payment" as processPayment
usecase "Verify Credit Card" as verifyCreditCard

customer --> placeOrder
placeOrder ..> processPayment : <<include>>
processPayment ..> verifyCreditCard : <<include>>

paymentGateway -- processPayment

@enduml
```