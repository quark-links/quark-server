package uk.vh7.common;

import org.hashids.Hashids;
import org.springframework.beans.factory.annotation.Value;

import java.util.Optional;

public class IDConverter {

    private Hashids hashids;

    @Value("${vh7.short-url-salt}")
    private String salt;

    public IDConverter() {
        String characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~";
        hashids = new Hashids(salt, 0, characters);
    }

    public String idToAlphaId(long id) {
        return hashids.encode(id);
    }

    public Optional<Long> alphaIdToId(String shortLink) {
        long[] ids = hashids.decode(shortLink);
        if (ids.length <= 0) { return Optional.empty(); }
        return Optional.of(ids[0]);
    }
}
