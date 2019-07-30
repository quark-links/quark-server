package uk.vh7.service;

import org.springframework.data.domain.Example;
import org.springframework.stereotype.Service;
import uk.vh7.common.IDConverter;
import uk.vh7.model.ShortLink;
import uk.vh7.repository.ShortLinkRepository;

import java.util.Optional;

@Service
public class ShortLinkService {
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
        IDConverter idConverter = new IDConverter();
        Optional<Long> id = idConverter.alphaIdToId(alphaId);
        if (!id.isPresent()) { return Optional.empty(); }
        return findById(id.get());
    }
}
