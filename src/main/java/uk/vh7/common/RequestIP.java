package uk.vh7.common;

import javax.servlet.http.HttpServletRequest;

public class RequestIP {
    public static String getRequestIP(HttpServletRequest request) {
        String output;
        output = request.getHeader("X-FORWARDED-FOR");
        if (output == null) {
            output = request.getRemoteAddr();
        }
        return output;
    }
}
