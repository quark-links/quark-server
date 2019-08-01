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

package uk.vh7.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Example;
import org.springframework.stereotype.Service;
import uk.vh7.common.IDConverter;
import uk.vh7.model.ShortLink;
import uk.vh7.repository.ShortLinkRepository;

import java.util.Optional;

@Service
public class ShortLinkService {
    @Autowired
    IDConverter idConverter;

    private final ShortLinkRepository shortLinkRepository;

    public ShortLinkService(ShortLinkRepository shortLinkRepository) {
        this.shortLinkRepository = shortLinkRepository;
    }

    public Optional<ShortLink> findById(Long id) {
        return shortLinkRepository.findById(id);
    }

    public ShortLink save(ShortLink shortLink) {
        // Check for duplicates
        ShortLink shortLink1 = new ShortLink();
        shortLink1.setLongUrl(shortLink.getLongUrl());
        Optional<ShortLink> duplicate = shortLinkRepository.findOne(Example.of(shortLink1));

        // If there is a duplicate, return that or save the new link and return that
        return duplicate.orElseGet(() -> shortLinkRepository.save(shortLink));
    }

    public Optional<ShortLink> findByAlphaId(String alphaId) {
        Optional<Long> id = idConverter.alphaIdToId(alphaId);
        if (!id.isPresent()) { return Optional.empty(); }
        return findById(id.get());
    }
}
