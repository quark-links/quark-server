package uk.vh7.common;

import org.hashids.Hashids;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.Optional;

@Component
public class IDConverter {
    private static String characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~";

    @Value("${vh7.short-url-salt}")
    String salt;

    public Hashids getHashids() {
        return new Hashids(salt, 0, characters);
    }

    public String idToAlphaId(long id) {
        return getHashids().encode(id);
    }

    public Optional<Long> alphaIdToId(String shortLink) {
        long[] ids = getHashids().decode(shortLink);
        if (ids.length != 1) { return Optional.empty(); }
        return Optional.of(ids[0]);
    }

    public String getShortLink(Identifiable entity) {
        return idToAlphaId(entity.getId());
    }
}
