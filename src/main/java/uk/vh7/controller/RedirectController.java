package uk.vh7.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.servlet.view.RedirectView;
import uk.vh7.exception.ShortLinkNotFoundException;
import uk.vh7.model.ShortLink;
import uk.vh7.service.ShortLinkService;

import java.util.Optional;

@Controller
public class RedirectController {
    private final ShortLinkService shortLinkService;

    public RedirectController(ShortLinkService shortLinkService) {
        this.shortLinkService = shortLinkService;
    }

    @GetMapping("/{alphaId}")
    public RedirectView shortLinkRedirect(@PathVariable String alphaId) {
        Optional<ShortLink> shortLink = shortLinkService.findByAlphaId(alphaId);
        if (!shortLink.isPresent()) {
            throw new ShortLinkNotFoundException(alphaId);
        }

        RedirectView redirectView = new RedirectView();
        redirectView.setUrl(shortLink.get().getLongUrl());
        return redirectView;
    }
}
