/*
 *     This file is part of VH7.
 *
 *     VH7 is free software: you can redistribute it and/or modify
 *     it under the terms of the GNU General Public License as published by
 *     the Free Software Foundation, either version 3 of the License, or
 *     (at your option) any later version.
 *
 *     VH7 is distributed in the hope that it will be useful,
 *     but WITHOUT ANY WARRANTY; without even the implied warranty of
 *     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *     GNU General Public License for more details.
 *
 *     You should have received a copy of the GNU General Public License
 *     along with VH7.  If not, see <https://www.gnu.org/licenses/>.
 */

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
