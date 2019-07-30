package uk.vh7.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value= HttpStatus.NOT_FOUND)
public class ShortLinkNotFoundException extends RuntimeException {

    public ShortLinkNotFoundException(String alphaId) {
        super(String.format("Short link '%s' was not found", alphaId));
    }
}
