package uk.vh7.api;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import uk.vh7.exception.ShortLinkNotFoundException;
import uk.vh7.model.ShortLink;
import uk.vh7.service.ShortLinkService;

import javax.servlet.http.HttpServletRequest;
import javax.validation.Valid;
import java.util.Optional;

import static uk.vh7.common.RequestIP.getRequestIP;

@RestController
@RequestMapping("/api/v1/shortlink")
public class ShortLinkAPI {
    private final ShortLinkService shortLinkService;

    public ShortLinkAPI(ShortLinkService shortLinkService) {
        this.shortLinkService = shortLinkService;
    }

    @PostMapping
    public ResponseEntity create(@Valid @RequestBody ShortLink shortLink, HttpServletRequest request) {
        shortLink.setCreatorIp(getRequestIP(request));
        return ResponseEntity.ok(shortLinkService.save(shortLink));
    }

    @GetMapping("/{alphaId}")
    public ResponseEntity<ShortLink> findById(@PathVariable String alphaId) {
        Optional<ShortLink> shortLink = shortLinkService.findByAlphaId(alphaId);
        if (!shortLink.isPresent()) {
            throw new ShortLinkNotFoundException(alphaId);
        }
        return ResponseEntity.ok(shortLink.get());
    }
}
