package com.aula.devops.controllers;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class MainController {

  @GetMapping("/hello")
  public String getHelloWorld() {
    return "Hello World";
  }

  @GetMapping("/hello/{nome}")
  public String getHelloNome(@PathVariable String nome) {
    return String.format("Hello, %s", nome);
  }

}
