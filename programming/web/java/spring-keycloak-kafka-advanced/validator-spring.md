# Note about validate

Validate properties in objects when they are null, and exeeced value, empty.

Spring support validator by this dependencies:

```
<dependency> 
    <groupId>org.springframework.boot</groupId> 
    <artifactId>spring-boot-starter-validation</artifactId> 
</dependency>
```

EX:

```
@Entity
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;
    
    @NotBlank(message = "Name is mandatory")
    private String name;
    
    @NotBlank(message = "Email is mandatory")
    private String email;
    
    // standard constructors / setters / getters / toString 
}
```

For validation object when it is passed to method you must be annotated @Valid in that method:

```
ResponseEntity<String> addUser(@Valid @RequestBody User user) {
        // persisting the user
        return ResponseEntity.ok("User is valid");
    }
```

If it occur error then it'll throw an exception: `MethodArgumentNotValidException `

To handle exception is thrown we using `@ExceptionaHandler` for catching exception:

```
@ResponseStatus(HttpStatus.BAD_REQUEST)
@ExceptionHandler(MethodArgumentNotValidException.class)
public Map<String, String> handleValidationExceptions(
  MethodArgumentNotValidException ex) {
    Map<String, String> errors = new HashMap<>();
    ex.getBindingResult().getAllErrors().forEach((error) -> {
        String fieldName = ((FieldError) error).getField();
        String errorMessage = error.getDefaultMessage();
        errors.put(fieldName, errorMessage);
    });
    return errors;
}
```

- Above annotation only for specific list of exceptions

- To centralize where exception is handled we use `@ControllerAdvice` and it will capture all exception, in case thrown an exception so that itsn't handle then it throw your application err



# Common annotation with validation

- @NotNull: Ensures a field is not null.
- @NotBlank: Enforces non-nullity and requires at least one non-whitespace character.
- @NotEmpty: Guarantees that collections or arrays are not empty.
- @Min(value): Checks if a numeric field is greater than or equal to the specified minimum value.
- @Max(value): Checks if a numeric field is less than or equal to the specified maximum value.
- @Size(min, max): Validates if a string or collection size is within a specific range.
- @Pattern(regex): Verifies if a field matches the provided regular expression.
- @Email: Ensures a field contains a valid email address format.
- @Digits(integer, fraction): Validates that a numeric field has a specified number of integer and fraction digits.
- @Past and @Future : Checks that a date or time field is in the past and future respectively.
- @AssertTrue and @AssertFalse: Ensures that a boolean field is true. and false respectively.
- @CreditCardNumber: Validates that a field contains a valid credit card number.
- @Valid: Triggers validation of nested objects or properties.
- @Validated: Specifies validation groups to be applied at the class or method level.

When appliy @Valid to method parameter => it will validate object before method is called

## Validation on nested properties

```
public class Order {
    @NotNull
    private String orderId;
    @Valid
    private ShippingAddress shippingAddress;
    // Other properties, getters, setters...
}
```

```
public class ShippingAddress {
    @NotNull
    private String street;
    @NotNull
    @Size(min = 2, max = 50)
    private String city;
    @NotNull
    private String zipCode;
}
```

```
@RestController
@RequestMapping("/api/users")
public class UserController {
    @PostMapping
    public ResponseEntity<String> createUser(@RequestBody @Valid User user, BindingResult bindingResult) {
        if (bindingResult.hasErrors()) {
            // Handle validation errors
            return ResponseEntity.badRequest().body("Validation errors found.");
        }
        // Process user and create a new user
        // ...
        return ResponseEntity.ok("User created successfully.");
    }
}
```

- If you dont pass `BindingResult` => if invalid => thrown exception and your method controller can't be called



# Custom validation

Is created by defining a new annotation => specifies the validation rules that you want to apply to fields or methods.
 
- @Target: => where annotation can be applied
- @Retention: what enviroment it is available
- @Constraint: => Specifies the validator class responsible for implementing the validation.

```
@Target({ElementType.FIELD, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = CustomValidator.class)
public @interface CustomValidation {
    String message() default "Invalid value";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
```

Class for implementing validation will implement interface `ConstraintValidator<Annotation, String>`

Use custom validation:

```
@CustomValidation
private String customField;
```

For class level validation and field validation so field will be validated in advanced.

# Validation groups
# Validation services
# BindingResult(above)

# References

<a href='https://medium.com/@dinesharney/advanced-bean-validation-techniques-for-clean-java-code-part-2-66b443ff79f7'>Custom validation </a>