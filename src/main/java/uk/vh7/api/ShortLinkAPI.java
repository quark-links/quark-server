package uk.vh7.api;

import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import uk.vh7.common.IDConverter;
import uk.vh7.common.Properties;
import uk.vh7.dto.ShortLinkDto;
import uk.vh7.exception.ShortLinkNotFoundException;
import uk.vh7.model.ShortLink;
import uk.vh7.service.ShortLinkService;

import javax.servlet.http.HttpServletRequest;
import javax.validation.Valid;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.Optional;

import static uk.vh7.common.RequestIP.getRequestIP;

@RestController
@RequestMapping("/api/v1/shortlink")
public class ShortLinkAPI {
    @Autowired
    IDConverter idConverter;

    @Autowired
    Properties properties;

    private final ShortLinkService shortLinkService;
    private ModelMapper modelMapper;

    public ShortLinkAPI(ShortLinkService shortLinkService) {
        this.shortLinkService = shortLinkService;
        this.modelMapper = new ModelMapper();
    }

    @PostMapping
    public ResponseEntity create(@Valid @RequestBody ShortLink shortLink, HttpServletRequest request) throws URISyntaxException {
        shortLink.setCreatorIp(getRequestIP(request));
        return ResponseEntity.ok(convertToDto(shortLinkService.save(shortLink)));
    }

    @GetMapping("/{alphaId}")
    public ResponseEntity<ShortLinkDto> findById(@PathVariable String alphaId) throws URISyntaxException {
        Optional<ShortLink> shortLink = shortLinkService.findByAlphaId(alphaId);
        if (!shortLink.isPresent()) {
            throw new ShortLinkNotFoundException(alphaId);
        }
        return ResponseEntity.ok(convertToDto(shortLink.get()));
    }

    private ShortLinkDto convertToDto(ShortLink shortLink) throws URISyntaxException {
        ShortLinkDto shortLinkDto = modelMapper.map(shortLink, ShortLinkDto.class);
        String shortLink1 = idConverter.getShortLink(shortLink);
        URI shortLinkUri = new URI(properties.getBaseUrl());
        shortLinkDto.setShortLink(shortLinkUri.resolve(shortLink1).toString());
        return shortLinkDto;
    }

    private ShortLink convertToEntity(ShortLinkDto shortLinkDto) {
        return modelMapper.map(shortLinkDto, ShortLink.class);
    }
}
