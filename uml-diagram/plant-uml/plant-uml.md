# What is plant-uml

Plant uml is a tool allow convert code to uml diagram.
It supports almost UML diagram such as: Sequence diagram, Usecase diagram, Class diagram, Activity diagram

For Sequence Diagram so plantUml code as pseuade code, it helpful to you when write code so that ignores case flow

Usually file PlantUml code has extension is *.pu, *.wsd, ...etc.

# Starting with PlantUml

- Download extensions PlantUml
- Write code
- To show preview diagram use combination key: Alt + D

# Code syntax

## Sample code

Code uml always place inside block @startuml and @enduml

```
@startuml

bob->alice: message # (arrow to connect two component in UML)
alice --> bob: message #(to write broken arrow using -->)

@enduml
```

## Declarative component

Although component we dont need declaration but you should declare it because you can easily visualize your system what do(who do):

Some keywords to declare such as:

- actor
- boudary
- control
- entity
- database
- collections
- queue

## Can chinh van ban

Căn chỉnh văn bản trên các mũi tên có thể được đặt sang trái, phải hoặc giữa bằng cách sử dụng `skinparam` `sequenceMessageAlign` , đặt nằm dưới tên sử dụng `skinparam` `responseMessageBelowArrow` `true`

# Dat page title, header, footer

Dùng các keyword title, header, footer để thêm title, header, footer cho diagram

## 4.6 Nhóm message

Có thể nhóm cácmessage lại với nhau bằng các từ khóa sau:

- alt/else
- opt
- loop
- par
- break
- critical
- group Có thể thêm một văn bản sẽ được hiển thị vào tiêu đề. Từ khóa end được sử dụng để đóng nhóm. Lưu ý rằng có thể lồng các nhóm.

## 4.7 Tạo ghi chú

Có thể ghi chú vào message bằng cách sử dụng từ khóa ghi chú note left hoặc note right bên phải ngay sau message. Bạn có thể có một ghi chú nhiều dòng bằng cách sử dụng các từ khóa end note.

# Class diagram

## Some declaring element

```
@startuml
abstract abstract
abstract class "abstract class"
interface interface
class class
class class_stereo <<stereotype>>
entity entity
@enduml
```

## Relations between classes

1. Extension => `<|--` 
2. Implementation => `<|..`
3. Composition => `*--`
4. Aggregation => `o--`
5. Dependency => `-->`
6. Dependency(weaker) => `..>`